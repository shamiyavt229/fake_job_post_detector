function JobInput({inputtext,setDesc}){
  
  return(
    <div>
      <h2>Paste Your Job Description</h2>

      <textarea className="jobinput"
        rows="10"
        cols="70"
        placeholder="Paste the job description here.."
        value={inputtext}
        onChange={(e)=>setDesc(e.target.value)}

        ></textarea>
    </div>
  );

}
export default JobInput;