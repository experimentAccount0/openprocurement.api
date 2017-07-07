��    &      L  5   |      P     Q     U     Y     ]     a     e     i     m     q     u  S   y  B   �       B       b     y  �   �  (   f  �   �  �   �  �   "  |   �  �   8	  O   �	  >    
  ;   _
  	   �
  *   �
  ;   �
  K        X  �   e     F  o   W  =   �  �     2   �  �  �     Q     U     Y     ]     a     e     i     m     q     u  �   y  ^     F   k  +  �  U   �  Q   4  o  �  >   �  i  5  
  �  $  �  �   �  �   �  �   �  �   )  �   �     �  F   �  ]   �  �   8     �    �  B   
  �   M  �      �   �   e   �!            &         #                         $      	          
                       %                                      !                                                   "    200 201 400 401 403 404 410 412 429 500 After processing API always provides response, reporting either success or failure. Archived. The resource requested is not and will not be available. Error Response Every successful get, create, update, replace request results in response that contains `data` attribute.  That `data` attribute contains full JSON object representation after the operation.  If some data were generated in the result of processing (like new object IDs, or `modified` date) they are present in the respose. Example Error Response Example Succes Response Forbidden. The API key and request syntax was valid but the server is refusing to complete the request.  This can happen if you are trying to read or write to objects or properties that you do not have access to. Here is a response that describes tender In all cases, the API should return an `HTTP Status Code <http://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_ that indicates the nature of the failure (see below), with a response body in JSON format containing additional information. In the event of an error, the response body will contain an `errors` field at the top level.  It contains an array of at least one error object, described below: Invalid request. This usually occurs because of a missing or malformed parameter.  Check the documentation and the syntax of your request and try again. No authorization. A valid API key was not provided with the request, so the API could not associate a user with the request. Not found. Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist. Part of the request causing the error. Possible values are `header` and `body`. Precondition Failed. See :ref:`API in cluster mode <cluster>`. Rate Limit Enforced. See :ref:`Rate control <performance>`. Responses Sample below indicates incomplete request. Server error. There was a problem on OpenProcurement's end. Specific header name that caused the problem (in case of `header` location) Status Codes Success (for object creation). Its information is available in the `data` field at the top level of the response body.  The API URL where the object can be retrieved is also returned in the `Location` header of the response. Success Response Success. If data was requested, it will be available in the `data` field at the top level of the response body. The field name causing the error (in case of `body` location) The listing requests result in similar responses, but instead of single object in `data` attribute, the JSON response contains collection of objects. Verbose (human readable) description of the error. Project-Id-Version: openprocurement.api 0.1
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2014-10-22 03:26+0300
PO-Revision-Date: 2016-02-12 17:32+0200
Last-Translator: Zoriana Zaiats <sorenabell@quintagroup.com>
Language-Team: Ukrainian <info@quintagroup.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: uk
X-Generator: Poedit 1.8.5
 200 201 400 401 403 404 410 412 429 500 Після обробки API завжди надає відповідь, звітуючи або про успіх, або про помилку. Архівовано. Шуканий ресурс не є й не буде доступним. Відповідь з повідомленням про помилку Кожен успішний запит вичитки, створення, оновлення, чи заміни отримує відповідь, що містить `data` атрибут. Цей  `data` атрибут містить повне представлення JSON об’єкта після операції. Якщо деякі дані були згенеровані у результаті обробки (наприклад, нові ID об’єкта або `modified` дата), то вони присутні у відповіді. Приклад відповіді з повідомленням про помилку Приклад відповіді з повідомленням про успіх Заборонено. API ключ та синтаксис запиту були дійсними, але сервер відмовляється виконати запит. Це може статися, якщо ви пробуєте прочитати або записати об'єкти чи властивості, до яких не маєте доступу. Це відповідь, що описує закупівлю. У будь-якому випадку API повинен повернути `Код стану HTTP <http://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_, що вказуватиме природу помилки (див. внизу), з тілом відповіді у форматі JSON, що міститиме додаткову інформацію. У випадку помилки, тіло відповіді міститиме `errors` поле на вищому рівні. Воно містить масив як мінімум одного помилкового об’єкта описаного нижче: Неправильний запит. Зазвичай це відбувається через відсутній або неправильний параметр. Перевірте документацію та синтаксис вашого запиту і спробуйте ще раз. Несанкційонований доступ. Не було надано дійсного API ключа разом із запитом, тому API не може зв'язати користувача із запитом. Ресурс не знайдено. Або даний метод та шлях запиту не вказують відому дію для API, або об’єкт, вказаний у запиті, не існує. Частина запиту спричинює помилку. Можливі значення це `header` (заголовок) або `body` (тіло). Збій під час обробки попередньої умови. Дивіться розділ :ref:`Pобота з API в режимі кластеру <cluster>`. Перевищено допустиму частоту запитів. Дивіться розділ :ref:`Контроль частоти запитів <performance>`. Відповіді Зразок нижче вказує на неповний запит. Помилка сервера. Була проблема зі сторони OpenProcurement. Конкретна назва заголовку, що спричиняє проблему (у випадку місцярозташування `заголовок`) Коди стану Створено. Його інформація доступна у `data` полі на верхньому рівні тіла відповіді. API URL, де об’єкт можна прочитати, міститься у `Location` заголовку відповіді. Відповідь з повідомленням про успіх Успіх. Якщо це був запит про інформацію, то вона буде доступна у `data` полі на верхньому рівні тіла відповіді. Конкретна назва поля, що спричиняє проблему (у випадку місцярозташування `тіло`) Запити списку отримують схожі відповіді, але замість одного об'єкта в `data` атрибуті, JSON відповідь містить колекцію об'єктів. Докладний (придатний для читання людиною) опис помилки. 