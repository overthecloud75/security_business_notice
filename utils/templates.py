def html_template(subject='', results=[]):
    html = '''
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Security Business Notice</title>
        <style>
            .vertical-table th, .vertical-table td {
                border: 1px solid #dddddd;
                padding: 7px;
            }
            .vertical-table th {
                background-color: #f2f2f2;
            }
            @media (max-width: 600px) {
                table {
                    display: block;
                }
                caption {
                    display: none;
                }
                thead {
                    display: none; /* 헤더 숨기기 */
                }
                tbody, tr, td {
                    display: block;
                    width: 100%;
                }
                tr {
                    margin-bottom: 16px; /* 각 데이터 그룹 간 간격 */
                }
                td {
                    position: relative;
                    padding-left: 50%; /* 헤더를 가상으로 표시할 공간 */
                }
            }
        </style>
    </head>
    <body style='font-family: Arial, sans-serif;'>
    '''

    html += f'''
    <div class='container' style='width: 100%; margin: auto; border-collapse: collapse; padding: 5px;'>
        <table class='vertical-table' style='width: 100%; border-collapse: collapse; margin: 10px 0;'>
            <caption style='font-size: 20px; font-weight: bold; color: #333; text-align: center; margin-bottom: 10px;'>{subject}</caption>
            <thead>
                <tr>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 6px;'>No</th>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 6px;'>출처</th>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 6px;'>타입</th>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 6px;'>Title</th>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 6px;'>수요</th>
                    <th style='text-align: center; background-color: #f2f2f2; border: 1px solid #dddddd; padding: 6px;'>Date</th>
                </tr>
            </thead>
            <tbody>
    '''
    for i, result in enumerate(results):
        if result['title']:
            html += f'''
                <tr>
                    <td style='text-align: center; border: 1px solid #dddddd; padding: 6px; align-items: center;'>{i + 1}</td>
                    <td style='text-align: center; border: 1px solid #dddddd; padding: 6px; align-items: center;'>{result['source']}</td>
                    <td style='text-align: center; border: 1px solid #dddddd; padding: 6px; align-items: center;'>{result['kind']}</td>
                    <td style='border: 1px solid #dddddd; padding: 6px; align-items: center;'>
                        <a href={result['href']}>{result['title']}</a>
                    </td>
                    <td style='text-align: center; border: 1px solid #dddddd; padding: 6px; align-items: center;'>{result['demand']}</td>                                                                                  
                    <td style='text-align: center; border: 1px solid #dddddd; padding: 6px; align-items: center;'>{result['date']}</td>
                </tr>
            '''
    html += '''
            </tbody>
        </table>
    '''
    return html 

