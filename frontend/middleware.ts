// middleware.ts : Redirect the user to the right locale + gate access before release date.
import { createI18nMiddleware } from 'next-international/middleware';
import { NextRequest, NextResponse } from 'next/server';

const I18nMiddleware = createI18nMiddleware({
  locales: ['fr'],
  defaultLocale: 'fr',
  urlMappingStrategy: 'rewriteDefault',
});

const RELEASE_DATE = new Date(process.env.NEXT_PUBLIC_RELEASE_DATE || '2025-02-18T10:00:00.000Z');
const SECRET_KEY = process.env.RELEASE_SECRET_KEY || '621fe232-753e-4b73-86d7-5f31bed3951d';
const ACCESS_COOKIE = 'team_access';

function isReleased(): boolean {
  return new Date() >= RELEASE_DATE;
}

export function middleware(request: NextRequest) {
  const { pathname, searchParams } = request.nextUrl;

  if (pathname === '/countdown' || pathname.startsWith('/countdown/')) {
    // If already released, redirect away from countdown to home
    if (isReleased()) {
      const url = request.nextUrl.clone();
      url.pathname = '/';
      url.search = '';
      return NextResponse.redirect(url);
    }
    return NextResponse.next();
  }

  // If the site is already released, let everyone through with i18n
  if (isReleased()) {
    return I18nMiddleware(request);
  }

  // use cookie to simplify multi routes handling
  const accessParam = searchParams.get('access');
  if (accessParam === SECRET_KEY) {
    const response = I18nMiddleware(request);
    response.cookies.set(ACCESS_COOKIE, 'true', {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      expires: RELEASE_DATE,
      path: '/',
    });
    return response;
  }

  // if request has cookie return like if it was released
  const hasAccess = request.cookies.get(ACCESS_COOKIE)?.value === 'true';
  if (hasAccess) {
    return I18nMiddleware(request);
  }

  // if try to reach any url and not released redirect to countdown
  const url = request.nextUrl.clone();
  url.pathname = '/countdown';
  url.search = '';
  return NextResponse.redirect(url);
}

export const config = {
  matcher: ['/((?!api|static|embed|.*\\..*|_next|favicon.ico|robots.txt).*)'],
};
