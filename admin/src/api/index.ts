import axios from "axios"
import { LoginType, RegisterType } from "../types/input"
import { User } from "../types/output";

const api =  axios.create({
    baseURL: import.meta.env.VITE_API_URL?.toString()
})

api.interceptors.request.use(
    function (config) {
        if (config.headers) {
            const store = localStorage.getItem('user')
            if(store){
                const user = JSON.parse(store) as User
                config.headers['Authorization'] = `Bearer ${user.access_token}`;
            }
        }
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);

export async function register(payload:RegisterType){
    const req = await api.post('/auth/register', payload)
    return req.data
}

export async function login(payload:LoginType){
    console.log(payload);
    
    const req = await api.post('/auth/login', payload)
    return req.data
}

export async function getUser(){
    const req = await api.get('/auth/me')
    return req.data
}

export async function fetchImages(){
    const req = await api.get('/medias')
    return req.data
}

export async function uploadImages(form: FormData){
    const req = await api.post(`/medias`, form)
    return req.data
}

export async function fetchClassificationStats(){
    const req = await api.get(`/medias/stats`)
    return req.data
}


