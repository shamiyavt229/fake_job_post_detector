import "./App.css";
import Navbar from "./components/navbar";
import JobInput from "./components/JobInput";
import PredictButton from "./components/PredictButton";
import PredictionCard from "./components/PredictionCard";
import CompanyEmail from "./components/companyEmail";
import WarningList from "./components/Warninglist";
import {useState} from "react";
function App(){
  const[email,setEmail]=useState("");
  const[description,setDescription]=useState("");
  const[prediction,setPrediction]=useState("");//prediction will get the prediction .it will say set prediction to change it.initially prediction is null .thats why state="".no-prediction wiil get prediction from the backend.i dont know why set prediction is there.beacuse react is not changing any data .it will be simmply updating whatever that it is getting from the backend
  const[confidence,setConfidence]=useState(""); 
  const[warnings,setWarnings]=useState([]); 
  const[error,setError]=useState("");
  //i dont know whhy[].we'll check it out later 
  return(
    <div className="App">
      <Navbar />

  

      <CompanyEmail 
      email={email}
      setEmail={setEmail}/>

      <JobInput 
      inputtext={description}
      setDesc={setDescription} />


      {error && (
        <p className="error-message">
          ⚠ {error}
        </p>
      )}

  
      <PredictButton 
      predicting={predict}/>

      <PredictionCard 
      prediction={prediction}
      confidence={confidence}
      /> {/*here there is no setprediction or set confidence.i think because it is just updating the info from backend unlike setDescription -setDescription func is updating the text we are writing  */}
      
      <WarningList 
      warnings={warnings}
      />
      

    </div>
  );

async function predict() {
  setError("");


  //clear previous result//
  setPrediction("");
  setConfidence("");
  setWarnings([]);
  
  const response= await fetch(
    "http://127.0.0.1:8000/api/predict/",
    {
      method:"POST",
      headers:{
        "Content-Type":"application/json",
      },
      body:JSON.stringify({
        company_email:email,
        description: description,
      }),

    }
  );
  const data = await response.json();

  if (!response.ok){
    setError(
      data.details?.description||
      data.details?.company_email||
      data.error||
      "Something went wrong"


    );
    return;
  }
  setPrediction(data.prediction);
  setConfidence(data.probability);//here setcofidence is a function that write the data to confidence.so the function first get the data .then only the confidence get it.but in case of input description get the data first ans set description is the function that writes it.the function input job is used because by typing in input box an event is happening.so it needs a function to handle it
  setWarnings(data.warnings || []);
  
}
}
export default App;