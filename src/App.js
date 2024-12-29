import './App.css';
import Body from './component/Body';
import { Provider } from 'react-redux';
import appStore from './Utils/appStore';

function App() {  
  return (
    <div className=''>
    <Provider store={appStore}>
      <Body/>
    </Provider>
    </div>
  );
}

export default App;
