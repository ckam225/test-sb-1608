import React from "react";
import { Image } from "../types/output";

type Props = {
    image: Image
}

function getUrl(url:string){
    return import.meta.env.VITE_IMAGE_BASE_URL?.toString()+ '/'+ url
}

const ImageItem:React.FC<Props> = ({image}) => {

    return <div className="flex flex-col image">
        {/* <div style={{padding: '5px'}}>
            <h2>{image.name}</h2>
            <h3>{image.category}</h3>
        </div> */}
        <img src={getUrl(image.url)} alt={image.category}/>
    </div>
}

export default ImageItem