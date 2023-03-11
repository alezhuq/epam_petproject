import CollapsibleList from "./CollapsibleList";
import { useState, useEffect } from "react";
import useCities from "../hooks/useCities";
import * as Checkbox from "@radix-ui/react-checkbox";
import { CheckIcon } from "@radix-ui/react-icons";
import { useSearchParams } from "react-router-dom";
import FilterToggle from "./FilterToggle";
import useCitiesStore from "../store/citiesStore";
export default function CitiesFilter() {
	const [search, setSearch] = useSearchParams();

	const filteredCities =
		search.getAll("city").map((elem) => parseInt(elem)) ?? [];

	const [cities, setCities] = useState(filteredCities);

	const getCities = useCities();
	const citiesData = useCitiesStore((state) => state.cities);
	const setCitiesData = useCitiesStore((state) => state.setCities);
	useEffect(() => {
		if (getCities.data) {
			setCitiesData(getCities.data);
		}
	}, [getCities.data]);

	const onCityChange = (city) => (checked) => {
		let _city = cities.slice();

		if (checked) {
			_city.push(city);
		} else {
			_city = _city.filter((_city) => _city !== city);
		}

		setCities(_city);
	};

	const hasFilters = filteredCities.length > 0;

	return (
		<CollapsibleList
			defaultVisible={true}
			title="Фільтр за містами"
			actionButton={
				<FilterToggle
					visible={cities.length > 0}
					active={hasFilters}
					onApply={() => {
						cities.forEach((elem) => {
							search.append("city", elem);
						});
						setSearch(search, {
							replace: true,
						});
					}}
					onClear={() => {
						search.delete("city");
						setCities([]);
						setSearch(search, {
							replace: true,
						});
					}}
				/>
			}
		>
			{citiesData
				.filter((f) => {
					if (filteredCities.length === 0) {
						return true;
					}
					return filteredCities.includes(f.id);
				})
				.map((field, key) => (
					<li key={key} className="pv2">
						<div className="flex items-center">
							<Checkbox.Root
								id={field.id}
								name={field.name}
								disabled={hasFilters}
								onCheckedChange={onCityChange(field.id)}
								checked={cities.includes(field.id)}
								className="checkbox lh-solid flex items-center justify-center pa0 bg-white w125 h125 br2 bn"
							>
								<Checkbox.Indicator>
									<CheckIcon className="checkbox__icon w125 h125" />
								</Checkbox.Indicator>
							</Checkbox.Root>
							<label htmlFor={field.name} className="ml3 fw5 f5">
								{field.name}
							</label>
						</div>
					</li>
				))}
		</CollapsibleList>
	);
}
