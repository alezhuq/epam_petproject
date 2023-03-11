import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Spring, animated } from "react-spring";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import { getOne, deleteOne } from "../../api/productsAPI";
import { useQuery } from "react-query";
import { PuffLoader } from "react-spinners";

function Product() {
	const { id } = useParams();
	const navigate = useNavigate();
	const { data, isLoading } = useQuery("getOneCompany", () => getOne(id));

	if (isLoading) {
		return (
			<div className="_container catalog__loading">
				<PuffLoader size={"350px"} cssOverride={{ marginTop: "150px" }} />
			</div>
		);
	}
	const [new_data] = data.data;

	function deleteCompany() {
		deleteOne(id);
		navigate("/");
	}

	return (
		<div className="product _container" id="product">
			<div className="product__content">
				<div className="product__imageblock">
					<Image
						key={process.env.API_URL + "/" + new_data.photo}
						photoSrc={process.env.API_URL + "/" + new_data.photo}
					/>
				</div>
				<div className="product__block">
					<h1 className="product__title">{new_data.name}</h1>
					<hr className="product__line" />
					<p>avg service price : {parseInt(new_data.companies_mean)} usd</p>
					<p className="product__description">{new_data.description}</p>
					<button onClick={deleteCompany} className="product__delete">
						delete
					</button>
				</div>
			</div>
			<h1 className="tc">Послуги компанії</h1>
			<ul className="products__list">
				{new_data.services.map((elem) => {
					return (
						<li className="product__elem" key={elem.name}>
							<p className="product__name">{elem.name}</p>
							<p className="product__desc">{elem.description}</p>
							<p className="product__price">{elem.price} usd</p>
						</li>
					);
				})}
			</ul>
		</div>
	);
}
function Image(props) {
	const { photoSrc } = props;

	return (
		<Spring
			from={{ opacity: 0 }}
			to={{ opacity: 1 }}
			config={{ duration: 1500 }}
		>
			{(props) => (
				<animated.div style={props}>
					<div>
						<img
							key={photoSrc}
							src={photoSrc}
							alt=""
							className="product__image"
							draggable="false"
						/>
					</div>
				</animated.div>
			)}
		</Spring>
	);
}

export default Product;
