import { useQuery } from "react-query";
import { $host } from "../api";

export default function useCities() {
	return useQuery(["city"], () => $host.get("city/").then((res) => res.data), {
		staleTime: 120000,
	});
}
