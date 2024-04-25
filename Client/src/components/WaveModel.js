import React, {useState} from 'react';
import axios from 'axios';
import '../index.css';


const WaveModel = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState('');

  const onFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const onUpload = async () => {
    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/upload/wave', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data.result);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };
  return (
    <div className="App">
      <h1>Wave Model</h1>
      <div className='container'>
        <div className='upload-file'>
        <input type="file" accept=".jpg, .jpeg, .png" onChange={onFileChange} />
        </div>
        <div className='upload-button'>
        <button class="button-85" onClick={onUpload}>Upload</button>
        </div>
        {result && <div className="result">{result}</div>}
      </div>
    </div>
  );
};

export default WaveModel;
