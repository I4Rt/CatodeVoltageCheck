/**
         * Делает POST-запрос на указанный URL с параметром vaultId
         * @param {number} vaultId - Идентификатор хранилища (vaultId)
         * @returns {Promise<object>} - Промис, который разрешается в объект с данными
         */
async function fetchVaultChartData(vaultId) {
    const url = `http://localhost:3031/getData?vaultId=${vaultId}`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (Array.isArray(data)) {
            const intervals = data.map(item => item.time_seconds); // Временные метки
            const values = data.map(item => item.value/FULL_TIME*ANGLE_AMMOUNT); // Значения
            return { intervals, values };
        } else {
            throw new Error('Received data is not an array');
        }
    } catch (error) {
        console.error('Ошибка при запросе данных:', error);
        throw error; // Прокидываем ошибку дальше
    }
}

/**
 * Функция отправляет POST-запрос на сервер, чтобы зарегистрировать изменение значения для определенного `vaultId`.
 *
 * @async
 * @function sendChangeEvent
 * @param {number} id - ID хранилища (vaultId), для которого необходимо зарегистрировать изменение.
 * @param {number} value - Значение, которое должно быть отправлено на сервер.
 * @returns {Promise<boolean>} - Возвращает `true`, если запрос успешен и сервер возвращает `"/addChangeEvent": true`, или `false`, если:

 * @throws {Error} - В случае ошибки сети или других проблем, связанных с выполнением запроса.
 */
async function sendChangeEvent(id, value) {
    const url = 'http://localhost:3031/addChangeEvent';
    const data = {
        vaultId: id,
        value: value
    };

    try {
        // Отправка POST-запроса
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // Проверяем, что код ответа 200 (OK)
        if (response.ok) {
            const result = await response.json();
            return result['/addChangeEvent'] || false; // Возвращаем true или false в зависимости от результата
        } else {
            return false; // Если код ответа не 200
        }
    } catch (error) {
        console.error('Error sending change event:', error);
        return false; // Возвращаем false в случае ошибки
    }
}


async function fetchResetVaultGate(id) {
    const url = `http://localhost:3031/resetVaultValue?vaultId=${id}`;
    console.log(123)
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            console.log('Возникла ошибка, перезагрузите страницу 1')
            return false;
        }

        const data = await response.json();
        return data['/resetVaultValue']
        
    } catch (error) {
        console.log('Возникла ошибка, перезагрузите страницу 2')
            return false;
    }

}

async function fetchExport(startTime, endTime){
    try {
        const response = await fetch(`http://localhost:3031/getEvents?startTime=${startTime}&endTime=${endTime}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            return false
        }

        // Получение бинарного содержимого ответа
        const blob = await response.blob();

        // Извлечение имени файла из заголовка Content-Disposition
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'events_export.zip'; // Имя по умолчанию

        if (contentDisposition) {
            const match = contentDisposition.match(/filename="?(.+?)"?$/);
            if (match && match[1]) {
                filename = match[1];
            }
        }

        // Создаем ссылку для скачивания файла
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        return true
    } catch (error) {
        console.error('Failed to fetch events:', error);
        return false
    }
};