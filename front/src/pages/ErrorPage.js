import React from "react";
import { Link } from "react-router-dom";
import "../styles/style.scss";

export default function ErrorPage({ title, text, link }) {
    return (
        <div className="error">
            <h1 className="error__title">{title}</h1>
            <div className="12">
                <Link to={link}>
                    <button className="button-9">
                        {text}
                    </button>
                </Link>
            </div>
        </div>
    );
}
