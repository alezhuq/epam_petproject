import React, { useState, useEffect } from "react";
import { postCompany } from "../api/productsAPI";
import useCompanies from "../hooks/useCompanies";
import useCompaniesStore from "../store/companiesStore";
import useCitiesStore from "../store/citiesStore";
import useCities from "../hooks/useCities";
import { PuffLoader } from "react-spinners";
const CreateCompany = () => {
	const getCities = useCities();
	const citiesData = useCitiesStore((state) => state.cities);
	const setCitiesData = useCitiesStore((state) => state.setCities);

	const getCompanies = useCompanies();
	const companiesData = useCompaniesStore((state) => state.companies);
	const setCompaniesData = useCompaniesStore((state) => state.setCompanies);

	const [name, setName] = useState("");
	const [description, setDescription] = useState("");
	const [website, setWebsite] = useState("");
	const [email, setEmail] = useState("");
	const [phonenum, setPhonenum] = useState("");
	const [photo, setPhoto] = useState("");
	const [cities, setCities] = useState([]);

	const [companyId, setCompanyId] = useState();
	const [updName, setUpdName] = useState("");
	const [updDescription, setUpdDescription] = useState("");
	const [updWebsite, setUpdWebsite] = useState("");
	const [updEmail, setUpdEmail] = useState("");
	const [updPhonenum, setUpdPhonenum] = useState("");
	const [updPhoto, setUpdPhoto] = useState("");
	const [updCities, setUpdCities] = useState([]);

	useEffect(() => {
		if (getCompanies.data) {
			setCompaniesData(getCompanies.data);
		}
		if (getCities.data) {
			setCitiesData(getCities.data);
		}
	}, [getCompanies.data, getCities.data]);
	if (getCompanies.isLoading) {
		return (
			<div className="_container catalog__loading">
				<PuffLoader size={"350px"} cssOverride={{ marginTop: "150px" }} />
			</div>
		);
	}

	function addCity() {
		setCities([...cities, { id: Date.now(), value: "" }]);
	}

	function handleChange(id, value) {
		setCities(
			cities.map((elem) => {
				if (elem.id === id) {
					return {
						...elem,
						["value"]: value,
					};
				}
				return elem;
			})
		);
	}

	function deleteCity(id) {
		setCities(
			cities.filter((elem) => {
				return elem.id !== id;
			})
		);
	}

	function addUpdCity() {
		setUpdCities([...updCities, { id: Date.now(), value: "" }]);
	}

	function handleUpdChange(id, value) {
		setUpdCities(
			updCities.map((elem) => {
				if (elem.id === id) {
					return {
						...elem,
						["value"]: value,
					};
				}
				return elem;
			})
		);
	}

	function deleteUpdCity(id) {
		setUpdCities(
			cities.filter((elem) => {
				return elem.id !== id;
			})
		);
	}

	function addCompany() {
		if (name && description && website && email && phonenum) {
			const str_cities = cities
				.map((elem) => {
					return elem.value;
				})
				.join(" ");
			postCompany(
				name,
				description,
				website,
				email,
				phonenum,
				photo,
				str_cities
			);
			setName("");
			setDescription("");
			setWebsite("");
			setEmail("");
			setPhonenum("");
			setPhoto(null);
			setCities([]);
		} else {
			alert("missing required data");
		}
	}
	function updateCompany() {
		putCompany(
			companyId,
			updName,
			updDescription,
			updWebsite,
			updEmail,
			updPhonenum,
			updPhoto
		);
		setUpdName("");
		setUpdDescription("");
		setUpdWebsite("");
		setUpdEmail("");
		setUpdPhonenum("");
		setUpdPhoto(null);
	}

	return (
		<div className="_container">
			<h1>Create Company</h1>
			<input
				className="field__input"
				placeholder="enter name..."
				value={name}
				onChange={(e) => setName(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter description..."
				value={description}
				onChange={(e) => setDescription(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter website..."
				value={website}
				onChange={(e) => setWebsite(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter email..."
				value={email}
				onChange={(e) => setEmail(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter phonenum..."
				value={phonenum}
				onChange={(e) => setPhonenum(e.target.value)}
			/>
			<br />

			<input
				className="field__input"
				type="file"
				accept="image/*"
				placeholder="enter photo..."
				onChange={(e) => {
					if (e.target.files) {
						setPhoto(e.target.files[0]);
					}
				}}
			/>
			<br />
			<button onClick={addCity} className="custom__button">
				add City
			</button>
			<br />
			{cities.map((elem, index) => {
				return (
					<div key={elem.id}>
						<p>City {index + 1}</p>
						<select onChange={(e) => handleChange(elem.id, e.target.value)}>
							<option value={null}>choose city...</option>;
							{citiesData.map((elem) => {
								return (
									<option key={elem.id} value={elem.id}>
										{elem.name}
									</option>
								);
							})}
						</select>
						<button
							onClick={() => deleteCity(elem.id)}
							className="custom__button"
						>
							delete City
						</button>
					</div>
				);
			})}
			<button onClick={addCompany} className="custom__button">
				Add Company
			</button>

			<br />
			<h1>Update Company</h1>

			<select
				onChange={(e) => setCompanyId(e.target.value)}
				value={companyId}
				className="products__sort"
			>
				<option value={null}>choose company...</option>;
				{companiesData.map((elem) => {
					return (
						<option key={elem.id} value={elem.id}>
							{elem.name}
						</option>
					);
				})}
			</select>
			<br />
			<input
				className="field__input"
				placeholder="enter name..."
				value={updName}
				onChange={(e) => setUpdUpdName(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter description..."
				value={updDescription}
				onChange={(e) => setUpdDescription(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter website..."
				value={updWebsite}
				onChange={(e) => setUpdWebsite(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter email..."
				value={updEmail}
				onChange={(e) => setUpdEmail(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter phonenum..."
				value={updPhonenum}
				onChange={(e) => setUpdPhonenum(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				type="file"
				accept="image/*"
				placeholder="enter photo..."
				searchbar__input
				onChange={(e) => {
					if (e.target.files) {
						setUpdPhoto(e.target.files[0]);
					}
				}}
			/>
			{updCities.map((elem, index) => {
				return (
					<div key={elem.id}>
						<p>City {index + 1}</p>
						<select onChange={(e) => handleUpdChange(elem.id, e.target.value)}>
							<option value={null}>choose city...</option>;
							{citiesData.map((elem) => {
								return (
									<option key={elem.id} value={elem.id}>
										{elem.name}
									</option>
								);
							})}
						</select>
						<button
							onClick={() => deleteUpdCity(elem.id)}
							className="custom__button"
						>
							delete City
						</button>
					</div>
				);
			})}
			<button onClick={addUpdCity} className="custom__button">
				add upd City
			</button>
			<br />
			<button onClick={updateCompany} className="custom__button">
				Update Company
			</button>
		</div>
	);
};

export default CreateCompany;
