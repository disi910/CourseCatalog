interface ErrorMessageProps {
  message: string;
}

export const ErrorMessage = ({ message }: ErrorMessageProps) => {
  return (
    <div className="retro-error">
      <p className="retro-error-title">!! Error !!</p>
      <p>{message}</p>
    </div>
  );
};
