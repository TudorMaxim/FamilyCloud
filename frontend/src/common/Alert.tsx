import styled from 'styled-components';

const Container = styled.div`
  position: absolute;
  margin: 8px;
  display: flex;
  justify-content: center;
  left: 0;
  width: -webkit-fill-available;
`;

type AlertProps = {
  type: 'primary' | 'success' | 'danger' | 'warning';
  message: string | null;
};

const Alert = ({ type, message }: AlertProps) => {
  if (!message) {
    return null;
  }
  return (
    <Container>
      <span role="alert" className={`alert alert-${type}`}>
        {message}
      </span>
    </Container>
  );
};

export default Alert;
