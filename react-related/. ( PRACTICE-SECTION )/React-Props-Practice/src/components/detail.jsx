import React from "react";

function ContactDisplayCard(props) {
    return (
        <div className="card">
            <div className="top">
                <p>{props.key}</p>
                <h2 className="name">{props.name}</h2>
                <img className="circle-img" src={props.image} alt="avatar_img" />
            </div>
            <div className="bottom">
                <p className="info">{props.phone}</p>
                <p className="info">{props.email}</p>
            </div>
        </div>
    );
}

export default ContactDisplayCard;
