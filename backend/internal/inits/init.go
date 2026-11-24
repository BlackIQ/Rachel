package inits

import "errors"

func Initialize() (err error) {
	if err := InitDotenv(); err != nil {
		return errors.New("[init.go] Init dotenv: " + err.Error())
	}

	if err := InitDB(); err != nil {
		return errors.New("[init.go] Init database: " + err.Error())
	}

	return nil
}
