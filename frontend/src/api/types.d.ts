export type UserCredentials = {
  email: string;
  password: string;
};

export type UserRegistrationData = UserCredentials & {
  firstName: string;
  lastName: string;
};
