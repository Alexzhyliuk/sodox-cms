from django.shortcuts import redirect, render
from django.urls import reverse
import pandas as pd
import functools


def upload_csv(custom={"success": "", "title": ""}):
    
    def decorator(funct):
        @functools.wraps(funct)
        def wrapper(request):
            if not(request.user.is_superuser):
                return redirect(reverse("products:index"))

            if request.POST:

                try:

                    data = request.FILES.get("csv_file")

                    if data:

                        csv_file = request.FILES['csv_file']
                        if not csv_file.name.endswith('.csv'):
                            return render(request, 'products/csv_upload.html', {"message": "Загружен не csv файл!"})

                        try:
                            if request.POST.get('sep'):
                                file = pd.read_csv(csv_file, sep=';')
                            else:
                                file = pd.read_csv(csv_file)

                        except Exception as e:
                            print(e)
                            return render(request, 'products/csv_upload.html', {"message": "Неверный разделитель"})

                        error_rows = []
                        for index, row in enumerate(file.iterrows()):

                            try:
                                funct(request, row)

                            except Exception as e:
                                print(e)
                                error_rows.append(index+1)

                        if error_rows:
                            return render(request, 'products/csv_upload.html', {"message": f"Ошибки в строках {error_rows}"})

                        return render(request, 'products/csv_upload.html', {"message": f"{custom['success']} успешно добавлены!"})

                    return render(request, 'products/csv_upload.html', {"message": "Проблема с файлом!"})


                except Exception as e:
                    return render(request, 'products/csv_upload.html', {"message": "Что-то пошло не так:("})

            return render(
                request,
                'products/csv_upload.html',
                {"message": '', "title": f"Добавить {custom['title']} через CSV"}
                )

        return wrapper

    return decorator
