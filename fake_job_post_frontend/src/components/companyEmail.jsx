function CompanyEmail({email,setEmail}){
  
  return(
    <div>
      

      <textarea className="email"
        rows="3"
        cols="70"
        placeholder="company Email"
        value={email}
        onChange={(e)=>setEmail(e.target.value)}

        ></textarea>
    </div>
  );

}
export default CompanyEmail;