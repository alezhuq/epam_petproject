import { $host } from ".";

export const getOne = async (id) => {
	return $host.get(`/company/${id}/`);
};

export const deleteOne = async (id) => {
	$host.delete(`/company/${id}/`);
	return;
};

export const deleteCity = async (id) => {
	$host.delete(`/city/${id}/`);
	return;
};

export const deleteService = async (id) => {
	$host.delete(`/service/${id}/`);
	return;
};

export const postCity = async (name) => {
	$host.post(`/city/`, { name: name });
	return;
};

export const postService = async (companyid, name, description, price) => {
	$host.post(`/service/`, {
		company_id: companyid,
		name: name,
		description: description,
		price: price,
	});
	return;
};

export const putService = async (id, name, description, price, company_id) => {
	$host.put(`/service/` + id + "/", {
		name: name,
		description: description,
		price: price,
		company_id: company_id,
	});
	return;
};

export const putCity = async (id, name) => {
	result = $host.put(`/city/` + id + "/", { name: name });
	return;
};

export const postCompany = async (
	name,
	description,
	website,
	email,
	phonenum,
	photo,
	cities
) => {
	const formData = new FormData();
	formData.append("name", name);
	formData.append("description", description);
	formData.append("website", website);
	formData.append("email", email);
	formData.append("phonenum", phonenum);
	formData.append("photo", photo);
	formData.append("cities", cities);
	$host.post(`/company/`, formData);
	return;
};

export const putCompany = async (
	id,
	name,
	description,
	website,
	email,
	phonenum,
	photo,
	cities
) => {
	const formData = new FormData();
	formData.append("name", name);
	formData.append("description", description);
	formData.append("website", website);
	formData.append("email", email);
	formData.append("phonenum", phonenum);
	formData.append("photo", photo);
	formData.append("cities", cities);
	$host.post(`/company/` + id + "/", formData);
	return;
};
