import React from "react";
import { GoogleMap, useLoadScript, Marker, InfoWindow} from "@react-google-maps/api";
import "../styles/style.scss";
import ErrorPage from "./ErrorPage";


const centerChortkiv = {lat: 49.013819102041445, lng: 25.798270239162633}
const centerCherkassy = {lat: 49.43341024806514, lng: 32.09031033864018}

function contacts() {
    const { isLoaded, loadError } = useLoadScript({
        googleMapsApiKey: process.env.REACT_API_KEY,
        language: 'uk'
    })

    if(!isLoaded) return (
        <div>
           <div className="lds-ring"><div></div><div></div><div></div><div></div></div>
        </div>
        )

    if(loadError) return <ErrorPage title={"Помилка при завантаженні GoogleMaps"} text={"Головне меню"} link={"/"}/>    

    return (
        <div className="contacts _container">
            <div className="contacts__block">
                <div className="contacts__text">
                    <h1>Чортків:</h1>
                        магазин "Бавовна"<br/>
                        м.Чортків, вул. Подільська, 35<br/>
                        Тел: +380685141364<br/>
                        e-mail: okytryk228@ukr.net
                </div>
                <div className="contacts__map">
                    <Map center = {centerChortkiv} lat = {49.009619102041445} lng = {25.798270239162633} description = " м.Чортків, вул. Подільська, 35"/>
                </div>
            </div>
            <div className="contacts__block">
                <div className="contacts__text">
                    <h1>Черкаси:</h1>
                        ТЦ "HIMARS"<br/>
                        м.Черкаси, вул. Волкова, 36<br/>
                        Тел: +380675551673<br/>
                        e-mail: pashashylo@ukr.net
                </div>
                <div className="contacts__map">
                    <Map center = {centerCherkassy} lat = {49.42941024806514} lng = {32.09031033864018} description = " м.Черкаси, вул. Волкова, 36"/>
                </div>
            </div>
        </div>
    )
}
function Map({center, lat, lng, description}) {
    return (
        <GoogleMap options={{streetViewControl: false, scaleControl: false, mapTypeControl: false, myLocationButtonEnabled: false, zoomControl: false, fullscreenControl: false}} zoom={13} center={center} mapContainerClassName="map">
            <Marker position={{lat: lat, lng: lng}}/>
               <InfoWindow position={center}><p className="tc">{description}</p></InfoWindow>
        </GoogleMap>
    )
}

export default contacts;