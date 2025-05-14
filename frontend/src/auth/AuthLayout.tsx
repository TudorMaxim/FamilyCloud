import { Outlet } from "react-router";
import styled from "styled-components";

const Container = styled.div`
    margin: 16px;
    display: flex;
    justify-content: center;
`;

const AuthLayout = () => (
    <Container>
        <Outlet />
    </Container>
);

export default AuthLayout;
