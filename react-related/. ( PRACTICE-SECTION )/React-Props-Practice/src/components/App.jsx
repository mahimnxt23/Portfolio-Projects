import React from "react";
import ContactDisplayCard from "./detail.jsx";
import contacts from "../contacts.js";


function showCard(contact) {
    return (
        <ContactDisplayCard
            key={contact.id}
            name={contact.name}
            image={contact.imgURL}
            phone={contact.phone}
            email={contact.email}
        />
    )
}


function App() {
    return (
        <div>
            <h1 className="heading">My Contacts</h1>
            {contacts.map(showCard)}
        </div>
    );
}

export default App;
