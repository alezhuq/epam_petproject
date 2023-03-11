import React, { useState, useEffect } from "react";
import { postService } from "../api/productsAPI";
import useCompanies from "../hooks/useCompanies";
import useServices from "../hooks/useServices";
import useCompaniesStore from "../store/companiesStore";
import { PuffLoader } from "react-spinners";

const CreateService = () => {
	const getCompanies = useCompanies();
	const companiesData = useCompaniesStore((state) => state.companies);
	const setCompaniesData = useCompaniesStore((state) => state.setCompanies);

	const getServices = useServices();
	const [services, setServices] = useState([]);

	const [serviceId, setServiceId] = useState();

	const [companyId, setCompanyId] = useState();
	const [serviceName, setServiceName] = useState();
	const [serviceDescr, setServiceDescr] = useState();
	const [servicePrice, setServicePrice] = useState();

	const [updCompanyId, setUpdCompanyId] = useState();
	const [updServiceName, setUpdServiceName] = useState();
	const [updServiceDescr, setUpdServiceDescr] = useState();
	const [updServicePrice, setUpdServicePrice] = useState();

	function addService() {
		if (serviceName && companyId && serviceDescr && servicePrice) {
			postService(companyId, serviceName, serviceDescr, servicePrice);
			setServiceName("");
			setServiceDescr("");
			setCompanyId("");
			setServicePrice(null);
		} else {
			alert("missing required data");
		}
	}
	function updateService() {
		postService(companyId, serviceName, serviceDescr, servicePrice, companyId);
		setUpdServiceName("");
		setUpdServiceDescr("");
		setUpdCompanyId("");
		setUpdServicePrice(null);
	}
	useEffect(() => {
		if (getCompanies.data && getServices.data) {
			setCompaniesData(getCompanies.data);
			setServices(getServices.data);
		}
	}, [getCompanies.data, getServices.data]);
	if (getCompanies.isLoading && getServices.isLoading) {
		return (
			<div className="_container catalog__loading">
				<PuffLoader size={"350px"} cssOverride={{ marginTop: "150px" }} />
			</div>
		);
	}

	return (
		<div className="_container">
			<h1>Create Service</h1>
			<select
				className="products__sort"
				onChange={(e) => setCompanyId(e.target.value)}
				value={companyId}
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
				placeholder="enter service name..."
				value={serviceName}
				onChange={(e) => setServiceName(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter service description..."
				value={serviceDescr}
				onChange={(e) => setServiceDescr(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter service price..."
				value={servicePrice}
				onChange={(e) => setServicePrice(parseInt(e.target.value))}
			/>
			<br />
			<button onClick={addService} className="custom__button">
				Add Service
			</button>
			<br />
			<select
				className="products__sort"
				onChange={(e) => {
					setServiceId(e.target.value);
				}}
				value={serviceId}
			>
				<br />
				<option value={null}>choose Service...</option>;
				{services.map((elem) => {
					return <option value={elem.id}>{elem.name}</option>;
				})}
			</select>
			<br />
			<input
				className="field__input"
				placeholder="enter service name..."
				value={updServiceName}
				onChange={(e) => setUpdServiceName(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter service description..."
				value={updServiceDescr}
				onChange={(e) => setUpdServiceDescr(e.target.value)}
			/>
			<br />
			<input
				className="field__input"
				placeholder="enter service price..."
				value={updServicePrice}
				onChange={(e) => setUpdServicePrice(parseInt(e.target.value))}
			/>
			<br />
			<button onClick={updateService} className="custom__button">
				Update Service
			</button>
		</div>
	);
};

export default CreateService;
