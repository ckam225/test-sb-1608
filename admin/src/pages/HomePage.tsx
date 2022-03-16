import React from 'react';
import { Navigate } from 'react-location';
import { fetchImages, uploadImages, fetchClassificationStats } from '../api';
import ImageCollection from '../components/ImageCollection';
import Stats from '../components/Stats';
import ImageUploadForm from '../components/ImageUploadForm';
import { useAuth } from '../hooks/auth';
import { ClassificationStat, Image } from '../types/output';


const HomePage = () => {

    const [images, setImages] = React.useState<Image[]>([])
    const [loading, setLoading] = React.useState(false)
    const [stats, setStats] = React.useState<ClassificationStat>()

    const {isAuthenticated} = useAuth()



    React.useEffect(() => {
        getImagesAsync()
        getClassificationStats()
    }, [])

    async function getImagesAsync() {
        setLoading(true)
        const res = await fetchImages()
        setImages(res || []) 
        setLoading(false)
    }


    async function getClassificationStats (){
        const st = await fetchClassificationStats()
        setStats(st)
    }
    

    async function handleImageUpload(form:FormData){
        const res = await uploadImages(form)
        getImagesAsync()
        getClassificationStats()
    }

    if(!isAuthenticated){
        return <Navigate to="/login" />
    }

    
    return <div className="container" style={{padding: "10px"}}>
        <div className="flex justify-between" style={{padding:"20px 0"}}>
           <ImageUploadForm onUpload={handleImageUpload}/>
           {stats && <Stats stats={stats}/>}
        </div>
        {loading ? <div>Loading...</div> : <ImageCollection images={images}/>}
    </div>
}
 
export default HomePage;