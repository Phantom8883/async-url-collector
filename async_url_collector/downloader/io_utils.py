def read_urls(path) -> list[str]:
    urls = []
    with open(path, 'r') as f:
        for line in f:
            clean = line.strip() # убирает пробелы и переносы строк по краям строки
            if not clean: # строки проверяем иначе, а не как сделал я: if clean != None:
                continue
            # if clean not in 'http://' or 'https://': # | - это не "или" для строк. Это побитовое OR, тут вообще не то.
            # startswith(...) проверяет ПРЕФИКС строки (начало строки).
            # Примеры:
            #   "https://site.com/file.jpg".startswith("https://") -> True
            #   "ftp://site.com".startswith("https://") -> False
            #
            # Тут мы хотим оставить только URL, которые начинаются с http:// или https://
            # Важный момент: нам нужна логика "НЕ http:// И НЕ https:// => пропустить".
            if not clean.startswith('http://') and not clean.startswith('https://'):
                continue
            else:
                urls.append(clean)
        return urls
