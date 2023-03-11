import React from "react";
import {useState, useEffect} from "react";

function line(){
    const useScrollPosition = () => {
        const [scrollPosition, setScrollPosition] = useState(0);
      
        useEffect(() => {
          const updatePosition = () => {
            setScrollPosition(window.pageYOffset);
          }
          window.addEventListener("scroll", updatePosition);
          updatePosition();
          return () => window.removeEventListener("scroll", updatePosition);
        }, []);
      
        return scrollPosition;
      };
    return <div className={useScrollPosition() >= 10 ? "line_after" : "line"}></div>
}
export default React.memo(line);