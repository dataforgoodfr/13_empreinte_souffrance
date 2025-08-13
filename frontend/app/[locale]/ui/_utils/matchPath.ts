export default (link: string, pathName: string, langSuffix: string) => {
  function isRoot(path: string) {
    return path === '/' || path === langSuffix;
  }
  function matchesPath(href: string, path: string) {
    return path.startsWith(`${langSuffix}${href}`) || path.startsWith(href);
  }

  return isRoot(link) ? isRoot(pathName) : matchesPath(link, pathName);
}
