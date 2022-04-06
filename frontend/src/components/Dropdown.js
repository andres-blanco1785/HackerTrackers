import React, {useRef, useState} from "react";
import "./Dropdown.css";
function Dropdown(props)
{
    const [isOpen, setIsOpen] = useState(false);
    const parentRef = useRef();

    return <div className="dropdown">
        <button className = "toggle" onClick = {() => setIsOpen(!isOpen)}>
            {props.label}
        </button>
        <div
            className = "content-parent"
            ref = {parentRef}
            style={
                isOpen
                    ? {
                        height: parentRef.current.scrollHeight + "px",
                    }
                    : {
                        height : "0px",
                    }
            }
        >
            <div className="content">
                {props.children}
            </div>
        </div>



    </div>
}

export default Dropdown;