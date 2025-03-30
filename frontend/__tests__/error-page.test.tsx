import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ErrorPage from '@/app/error';

describe('Error Page', () => {
  it('renders the error page with server error message', () => {
    const serverError = new Error('Server error occurred');
    (serverError as any).statusCode = 500;

    render(<ErrorPage error={serverError} reset={() => {}} />);

    expect(screen.getByText('Something went wrong!')).toBeInTheDocument();
    expect(screen.getByText('Try again')).toBeInTheDocument();
  });
});
