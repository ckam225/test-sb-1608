import React, { FormEvent } from 'react';
import * as api from '../api';
import { LoginType } from '../types/input';
import {Navigate, useNavigate} from 'react-location'
import { useAuth } from '../hooks/auth';

const LoginPage = () => {

    const [loading, setLoading] = React.useState(false)
    const navigate = useNavigate()


    const {isAuthenticated, setAuthUser} = useAuth()

    if(isAuthenticated){
        return <Navigate to="/"/>
    }

    const [values, setValues] = React.useState<LoginType>({
       username: '',
       password: ''
    })

    async function handleSubmit(e:FormEvent){
        e.preventDefault()
        try {
            setLoading(true)
            const res = await api.login(values)
            setAuthUser(res)
            return navigate({to:'/'})
        } catch (error) {
            alert('неверные логин и пароль')
        }
        finally {
            setLoading(false)
        }
    }

    function handleFieldChange(e:React.ChangeEvent<HTMLInputElement|HTMLSelectElement>){
        const newFormValue = {...values} as any
        newFormValue[e.target.name] = e.target.value
       setValues(newFormValue)
    }

    return <div className="login-bloc">
        <form className="form" onSubmit={handleSubmit}> 
            <h1>Авторизация</h1>
            <div className="form-group">
                <input type="text" className="input" required placeholder="Имя пользователь" name="username" onChange={handleFieldChange}/>
            </div>
            <div className="form-group">
                <input type="password" className="input" required  placeholder="Пароль"  name="password" onChange={handleFieldChange}/>
            </div>
            {!loading && <div className="form-group">
                <button className="btn" type="submit">Войти</button>
            </div>}
        </form>
    </div>
}
 
export default LoginPage;