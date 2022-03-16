import React, { FormEvent, useRef, useState } from "react";

type Props = {
    onUpload: (form: FormData) => {}
}

const ImageUploadForm:React.FC<Props> = ({onUpload}) => {

    const [files, setFiles] = useState<File[]>([]);
    const [category, setCategory] = useState('');

    function onFileChange(e:React.ChangeEvent<HTMLInputElement>) {
        const fileList = e.target.files
        if(fileList && fileList.length){
            setFiles(c => c.concat(Array.from(fileList)))
        }
    }

    function onInputChange(e:React.ChangeEvent<HTMLSelectElement>) {
       setCategory(e.target.value)
       console.log(e.target.value);
       
    }

    function onSubmit(e:FormEvent) {
        e.preventDefault()
        var formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i])
        }
        formData.append('category', category)
        onUpload(formData)
    }


    return <div className="row">
        <form onSubmit={onSubmit}>
            <h3>Загрузить фотографии</h3>
            <div className="flex items-center">
                <div className="form-group">
                    <input type="file" multiple onChange={onFileChange} className="input" required/>
                </div>
                <div className="form-group">
                    <select name="category" onChange={onInputChange} className="input" value={category}  required>
                        <option disabled>Выберете сущности</option>
                        <option value="Котик">Котик</option>
                        <option value="Собачка">Собачка</option>
                    </select>
                </div>
                <div className="form-group">
                    <button className="btn btn-primary" type="submit">Запустить в работу</button>
                </div>
             </div>
        </form>
    </div>
}
 
export default ImageUploadForm;