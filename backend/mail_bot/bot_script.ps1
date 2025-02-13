# Function to compress a string using GZip
function Compress-String {
    param(
        [string]$String
    )

    $Bytes = [System.Text.Encoding]::UTF8.GetBytes($String)
    $MemoryStream = New-Object System.IO.MemoryStream
    $GZipStream = New-Object System.IO.Compression.GZipStream($MemoryStream, [System.IO.Compression.CompressionMode]::Compress)
    $GZipStream.Write($Bytes, 0, $Bytes.Length)
    $GZipStream.Close()
    $CompressedBytes = $MemoryStream.ToArray()
    $MemoryStream.Close()
    [Convert]::ToBase64String($CompressedBytes)
}
# Function to decompress a GZip compressed string
function Decompress-String {
    param(
        [string]$CompressedString
    )
    $CompressedBytes = [Convert]::FromBase64String($CompressedString)
    $MemoryStream = New-Object System.IO.MemoryStream($CompressedBytes)
    $GZipStream = New-Object System.IO.Compression.GZipStream($MemoryStream, [System.IO.Compression.CompressionMode]::Decompress)
    $DecompressedBytes = New-Object System.IO.MemoryStream
    $GZipStream.CopyTo($DecompressedBytes)
    $GZipStream.Close()
    $MemoryStream.Close()
    [System.Text.Encoding]::UTF8.GetString($DecompressedBytes.ToArray())
}

# Output directory
$OutputDir = "C:\AlertData\CompressedMails" # Or any other path you prefer
$PythonPath = "C:\Users\sachin.bisht01\OneDrive - Infosys Limited\Desktop\makeathon\makeathon 18\TriageAssistant\.venv\Scripts\python.exe" # Path to your Python executable
$FaissScriptPath = "C:\Users\sachin.bisht01\OneDrive - Infosys Limited\Desktop\makeathon\makeathon 18\TriageAssistant\backend\mail_bot\faiss_script.py" # Path to your FAISS Python script

# Check if Python executable exists
if (!(Test-Path -Path $PythonPath)) {
    Write-Error "Python executable not found at: $PythonPath"
    return 
}

if (!(Test-Path -Path $FaissScriptPath)) {
    Write-Error "Faiss script not found at: $FaissScriptPath"
    return 
}

if (!(Test-Path -Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir
}

try {
    $OutlookProc = ( Get-Process | where { $_.Name -eq "OUTLOOK" } )
    if ( $OutlookProc -eq $null ) { 
        Start-Process outlook.exe -WindowStyle Hidden; 
        Start-Sleep -Seconds 5 
    }
    Add-Type -Assembly "Microsoft.Office.Interop.Outlook"
    $Outlook = New-Object -ComObject Outlook.Application
    $Namespace = $Outlook.GetNamespace("MAPI")
    $Inbox = $Namespace.GetDefaultFolder([Microsoft.Office.Interop.Outlook.OlDefaultFolders]::olFolderInbox)
    $MaxMails = 100
    $MailCount = 0
    $TotalItems = $Inbox.Items.Count
    for ($i = $TotalItems; $i -ge ($TotalItems - $MaxMails + 1); $i--) {
        try {
            $Mail = $Inbox.Items.Item($i)
            Write-Host "Processing mail: $($Mail.Subject)"
            $MailBody = if ($Mail.BodyFormat -eq 2) { $Mail.HTMLBody } else { $Mail.Body }
            if (-not [string]::IsNullOrEmpty($MailBody)) {
                
                # Sanitize filename
                $FileName = "$($Mail.Subject -replace '[\\/:*?"<>|]', '_')_compressed"
                $BaseFilePath = Join-Path -Path $OutputDir -ChildPath $FileName

                # Determine file extension based on body format
                $FileExtension = if ($Mail.BodyFormat -eq 2) { ".html"} else { ".txt" }
                $FilePath = $BaseFilePath + $FileExtension

                # Check if the file already exists. Append a counter if needed.
                $Counter = 1
                while (Test-Path -Path $FilePath) {
                    $FileName = "$($Mail.Subject -replace '[\\/:*?"<>|]', '_')_$Counter"
                    $FilePath = Join-Path -Path $OutputDir -ChildPath $FileName + $FileExtension
                    $Counter++
                }
                try {
                    # Save the mail content to the file
                    $MailBody | Out-File -FilePath $FilePath -Encoding UTF8
                    Write-Host "Mail saved to: $FilePath"
                }
                catch {
                    Write-Warning "Error saving mail '$($Mail.Subject)': $_"
                }
            } else {
                Write-Host "Mail body is empty."
            }
        }
        catch {
            Write-Warning "Error processing mail at index $i"
        }
    }
    # Release COM objects (VERY IMPORTANT!)
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Inbox)
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Namespace)
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Outlook)
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()

    Write-Host "Finished processing mails."

    try {
        # Run the Python script
        Write-Host "Running Faiss script..."
        & $PythonPath $FaissScriptPath # The & is the call operator in PowerShell
        Write-Host "Faiss script completed."
    }
    catch {
        Write-Error "Error running Faiss script: $_"
    }
}
catch {
    Write-Error "Error: $_"
    if ($_.Exception.GetType().FullName -eq "System.IO.FileNotFoundException") {
      Write-Warning "It's likely that the Outlook Interop Assembly is not available. Please ensure Office/Outlook is installed."
    }
}                                     