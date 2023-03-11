import {createRoot} from 'react-dom/client'
import App from './app';
import { QueryClientProvider } from 'react-query';
import { queryClient } from './api';

const root = createRoot(document.getElementById("root"));

root.render(
    <QueryClientProvider client={queryClient}>
            <App/>
    </QueryClientProvider>
)