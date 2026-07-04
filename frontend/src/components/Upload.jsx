import { useState } from "react";
import axios from "axios";

function Upload() {

  const [selectedFile, setSelectedFile] = useState(null);
const handleUpload = async () => {

    if (!selectedFile) {
        alert("Please select a PDF first.");
        return;
    }

    const formData = new FormData();

    formData.append("file", selectedFile);
    try {

    const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
    );

    alert(response.data.message);

}
catch(error){

    alert("Upload Failed!");

}

};

  return (
    <div>
      <h2>Upload PDF</h2>

      <input
        type="file"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>
  Upload
</button>

      <p>{selectedFile?.name}</p>
    </div>
  );
}

export default Upload;