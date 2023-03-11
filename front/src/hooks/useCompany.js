import { useQuery } from "react-query";
import { $host } from "../api";

export default function useCompany(id) {
	return useQuery(
		["company"],
		() => $host.get(`company/${id}/`).then((res) => res.data),
		{
			staleTime: 120000,
		}
	);
}
