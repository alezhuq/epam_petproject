import { useQuery } from "react-query";
import { $host } from "../api";

export default function useServices() {
	return useQuery(
		["services", "services"],
		() => $host.get("service/").then((res) => res.data),
		{
			staleTime: 120000,
		}
	);
}
