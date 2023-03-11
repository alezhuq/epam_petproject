import React, { useEffect } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { LazyLoadImage } from "react-lazy-load-image-component";
import SearchBar from "../components/SearchBar";
import useCompanies from "../hooks/useCompanies";
import { PuffLoader } from "react-spinners";
import useCompaniesStore from "../store/companiesStore";
import Sort from "../components/Sort";
import CitiesFilter from "../components/CitiesFilter";

function Catalog() {
	const [search, setSearch] = useSearchParams();

	const companies = useCompaniesStore((state) => state.companies);

	const setCompanies = useCompaniesStore((state) => state.setCompanies);

	const getCompanies = useCompanies();

	useEffect(() => {
		if (getCompanies.data) {
			setCompanies(getCompanies.data);
		}
	}, [getCompanies.data]);

	const allProducts = companies.map((pr) => {
		return (
			<li key={pr.id} className="product__elem">
				<Link to={"/product/" + pr.id}>
					<div className="product__name">{pr.name}</div>
					<div>
						<LazyLoadImage
							className="product__img"
							src={process.env.API_URL + "/" + pr.photo}
							effect="blur"
							draggable="false"
						/>
					</div>
				</Link>
			</li>
		);
	});

	return (
		<div className="products _container">
			<CitiesFilter />
			<div className="products__sort__catalog">
				<Sort
					onChange={(e) => {
						if (e.target.value === "") {
							search.delete("ordering");
							setSearch(search, {
								replace: true,
							});
							return;
						}
						search.set("ordering", e.target.value);
						setSearch(search, {
							replace: true,
						});
					}}
					defaultValue={search.get("ordering")}
					name="sort"
					options={[
						{
							label: "Без фільтрів",
							value: "",
						},
						{
							label: "A-Я",
							value: "name",
						},
						{
							label: "Я-А",
							value: "-name",
						},
					]}
				/>
			</div>
			<div className={"flex"}>
				{getCompanies.isLoading ? (
					<div className="_container catalog__loading">
						<PuffLoader size={"350px"} cssOverride={{ marginTop: "150px" }} />
					</div>
				) : (
					<ul className="products__list">{allProducts}</ul>
				)}
			</div>
		</div>
	);
}

export default Catalog;
