import { ReactLocation, createBrowserHistory, DefaultGenerics, Route, Navigate } from "react-location";
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'


export const location = new ReactLocation({
    history: createBrowserHistory()
})

export const routes: Route<DefaultGenerics>[] = [
  {
      path: '/',
      element: <HomePage/>
    },
    {
      path: '/login',
      element: <LoginPage/>
    },
    {
      path: '*',
      element: () => import('./pages/NotFoundPage')
          .then(module => (<module.default />))
    }
]
