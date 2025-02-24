
import { useAuthInit, useNoAuth } from "./auth.service";

const AuthFlowLayout = ({ children }: { children: React.ReactNode }) => {
    useNoAuth();
    useAuthInit();

    return (
        <div>
            {children}
        </div>
    );
};

export { AuthFlowLayout };
export default AuthFlowLayout;
