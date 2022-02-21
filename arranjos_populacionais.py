import ftplib
import os


def download_from_ibge(path, directory):
    """ Download zip files from IBGE """
    ftp = ftplib.FTP(path)
    ftp.login("anonymous", "arranjos")
    ftp.cwd(directory)
    files = ftp.nlst()

    for file in files:
        if ftp.size(file) is not None:
            with open(os.path.join('data/arranos', file), 'wb') as f:
                ftp.retrbinary('RETR ' + file, f.write)
                print(f'... downloading {file}')
        else:
            ftp.cwd(file)
            print(f'... going into {file} directory')
            download_from_ibge(path, os.path.join(directory, file))
            print(f'coming back')
            ftp.cwd('..')


if __name__ == '__main__':
    p = 'geoftp.ibge.gov.br'
    d = 'organizacao_do_territorio/divisao_regional/arranjos_populacionais/tabelas_xls_2ed/'
    download_from_ibge(p, d)
