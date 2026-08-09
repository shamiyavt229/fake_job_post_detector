function WarningList({warnings}){


  if (warnings.length===0){
    return null;

  }
  return(
    <div>
      <h3>
        Warnings
      </h3>
      <p>⚠ {warnings[0]}</p>

    </div>

  );

}
export default WarningList;