import matchPath from './matchPath';

describe('matchPath', () => {
  describe('root link cases', () => {
    const langSuffix = '/fr';

    test.each([
      ['/', '/', true],
      ['/', '/fr', true],
      ['/fr', '/', true],
      ['/', '/about', false],
    ])('link=%s, pathName=%s → %s', (link, pathName, expected) => {
      expect(matchPath(link, pathName, langSuffix)).toBe(expected);
    });
  });

  describe('non-root link cases', () => {
    const langSuffix = '/fr';

    test.each([
      ['/about', '/about', true],
      ['/about', '/fr/about', true],
      ['/about', '/contact', false],
    ])('link=%s, pathName=%s → %s', (link, pathName, expected) => {
      expect(matchPath(link, pathName, langSuffix)).toBe(expected);
    });
  });

  describe('different languages', () => {
    const esSuffix = '/es';

    test.each([
      ['/', '/es', true],
      ['/about', '/es/about', true],
    ])('link=%s, pathName=%s → %s', (link, pathName, expected) => {
      expect(matchPath(link, pathName, esSuffix)).toBe(expected);
    });
  });
});
