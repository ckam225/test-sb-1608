import { Outlet, Router } from 'react-location'
import { routes, location } from './router'


function App() {
  return <Router routes={routes} location={location}>
     <Outlet/>
  </Router>
}

export default App
