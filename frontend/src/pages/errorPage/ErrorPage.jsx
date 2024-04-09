import "./ErrorPage.css";

export default function ErrorPage({error}) {
  console.error(error);

  return (
    <div id="error-page">
      <h1 className="error-title">Oops!</h1>
      <p className="error-text">Sorry, an unexpected error has occurred.</p>
      <p className="error-text">
        {/* <i>{error.statusText || error.message}</i> ЕЩЕ ОДНА ЗАГЛУШКА */}
        <i>{error || error}</i>
      </p>
    </div>
  );
}