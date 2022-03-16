import React,  {useEffect, useMemo, useState} from 'react'
import { User } from '../types/output'


function getFromLocal(): User {
    const u  = localStorage.getItem('user')
    if(u){
        return  JSON.parse(u) as User
    }
    return null as unknown as User
}

export const useAuth = () => {

    const [authUser, setAuthLocalUser] = useState<User>(getFromLocal())

    const isAuthenticated = useMemo(() => authUser != null || authUser != undefined, [authUser])

    function setAuthUser(user:User){
        localStorage.setItem('user', JSON.stringify(user))
        setAuthLocalUser(user)
    }

    return {
        isAuthenticated,
        setAuthUser,
        authUser
    }
}
