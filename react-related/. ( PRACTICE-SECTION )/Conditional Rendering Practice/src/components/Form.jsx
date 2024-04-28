import React from "react";
import ShowField from "./InputField";


function Form(props) {
    return (
        <form className="form">
            <ShowField type="text" placeholder="Username" />
            <ShowField type="password" placeholder="Password" />
            {!props.isRegistered ? <ShowField type="password" placeholder="Confirm Password" /> : null}
            <button type="submit">{props.isRegistered ? "Login" : "Register"}</button>
        </form>
    );
}

export default Form;
