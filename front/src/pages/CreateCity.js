import React, { useState, useEffect } from "react";
import { postCity, putCity, deleteCity } from "../api/productsAPI";
import useCitiesStore from "../store/citiesStore";
import useCities from "../hooks/useCities";
import { PuffLoader } from "react-spinners";
const CreateCity = () => {
	const getCities = useCities();
	const citiesData = useCitiesStore((state) => state.cities);
	const setCitiesData = useCitiesStore((state) => state.setCities);
	const [city, setCity] = useState();

	const [delId, setDelId] = useState();
	const [changeCity, setChangeCity] = useState();
	const [cityId, setCityId] = useState();
	useEffect(() => {
		if (getCities.data) {
			setCitiesData(getCities.data);
		}
	}, [getCities.data]);
	if (getCities.isLoading) {
		return (
			<div className="_container catalog__loading">
				<PuffLoader size={"350px"} cssOverride={{ marginTop: "150px" }} />
			</div>
		);
	}

	function addCity() {
		if (city) {
			postCity(city);
			setCity("");
		} else {
			alert("missing required data");
		}
	}

	function updateCity() {
		if (changeCity && cityId) {
			putCity(cityId, changeCity);
			setCityId(null);
			setChangeCity("");
		} else {
			alert("missing required data");
		}
	}

	function delCity() {
		if (delId) {
			deleteCity(delId);
			setDelId(null);
		} else {
			alert("missing required data");
		}
	}

	return (
		<div className="_container">
			<h1>Add City</h1>
			<input
				className="field__input"
				placeholder="enter name..."
				value={city}
				onChange={(e) => setCity(e.target.value)}
			/>
			<br />
			<button onClick={addCity} className="custom__button">
				Add
			</button>
			<br />
			<br />
			<br />
			<h1>Change City</h1>
			<br />
			<select
				className="products__sort"
				onChange={(e) => {
					setCityId(e.target.value);
				}}
				value={cityId}
			>
				<option value={null}>choose City...</option>;
				{citiesData.map((elem) => {
					return <option value={elem.id}>{elem.name}</option>;
				})}
			</select>
			<br />
			<input
				className="field__input"
				placeholder="enter name..."
				value={changeCity}
				onChange={(e) => setChangeCity(e.target.value)}
			/>
			<br />
			<button onClick={updateCity} className="custom__button">
				Update
			</button>
			<br />
			<h1>Delete City</h1>
			<br />
			<select
				className="products__sort"
				onChange={(e) => {
					setDelId(e.target.value);
				}}
				value={delId}
			>
				<option value={null}>choose City...</option>;
				{citiesData.map((elem) => {
					return <option value={elem.id}>{elem.name}</option>;
				})}
			</select>
			<button onClick={delCity} className="product__delete">
				delet eCity
			</button>
			<br />
		</div>
	);
};

export default CreateCity;
