import React from 'react';
import {Image} from '../types/output'
import ImageItem from './ImageItem';



type Props = {
    images: Image[]
}

const ImageCollection:React.FC<Props> = ({images=[]}) => {
    return <div className="grid grid-4" >
        {images.map((image) => <ImageItem image={image} key={image.id}/>)}
    </div>
}
 
export default ImageCollection;