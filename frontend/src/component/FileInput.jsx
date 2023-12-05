import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone';

const FileInput = () => {
    const [files, setFiles] = useState([]);

    const onDrop = useCallback((acceptedFiles) => {
      setFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
    }, []);
    
    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });
    return (
        <div>
          <div {...getRootProps()} className='border-dashed border-[2px] border-cyan-800 w-[70%] h-16 flex-center rounded-lg cursor-pointer'>
            <input {...getInputProps()} />
            {isDragActive ? (
              <p>Drop the files here...</p>
            ) : (
              <p>Drag 'n' drop some CV's here, or click to select files</p>
            )}
          </div>
          <ul className='mt-6 flex flex-col w-[70%] border-2 border-cyan-800 rounded-lg'>
            {files.map((file) => (
              <li className=' border-[1px] border-cyan-600 h-8 flex-center' key={file.name}>{file.name}</li>
            ))}
          </ul>
        </div>
      );
};


export default FileInput