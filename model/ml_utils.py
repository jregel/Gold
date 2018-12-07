
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

def print_dataframe_summary(df):
    print('---------- DataFrame Info ----------')
    print(df.info())

    print('\n')

    print('---------- DataFrame Shape ----------')
    print(df.shape)
    print('\n')

    print('---------- DataFrame Index ----------')
    print(df.index)
    print('\n')

    print('---------- DataFrame Columns ----------')
    print(df.columns)
    print('\n')

    print('---------- DataFrame Description ----------')
    print(df.describe())
    print('\n')

    print('---------- DataFrame Head ----------')
    print(df.head())
    print('\n')

    return 

def model_comparison(X_train, X_test, y_train, y_test):
	# Construct  pipelines
	pipe_lr = Pipeline([('scl', StandardScaler()),
				('clf', LogisticRegression(random_state=42))])

	pipe_lr_pca = Pipeline([('scl', StandardScaler()),
				('pca', PCA(n_components=3)),
				('clf', LogisticRegression(random_state=42))])

	pipe_rf = Pipeline([('scl', StandardScaler()),
				('clf', RandomForestClassifier(random_state=42))])

	pipe_rf_pca = Pipeline([('scl', StandardScaler()),
				('pca', PCA(n_components=3)),
				('clf', RandomForestClassifier(random_state=42))])

	pipe_svm = Pipeline([('scl', StandardScaler()),
				('clf', svm.SVC(random_state=42))])

	pipe_svm_pca = Pipeline([('scl', StandardScaler()),
				('pca', PCA(n_components=3)),
				('clf', svm.SVC(random_state=42))])
				
	# Set grid search params
	param_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	param_range_fl = [10, 1.0, 0.5, 0.1, 0.01, 0.001]
	gamma = [0.001, 0.01, 0.1, 1]

	grid_params_lr = [{'clf__penalty': ['l1', 'l2'],
			'clf__C': param_range_fl,
			'clf__solver': ['liblinear', 'saga']}] 

	grid_params_rf = [{'clf__criterion': ['gini', 'entropy'],
			'clf__min_samples_leaf': param_range,
			'clf__max_depth': param_range,
			'clf__min_samples_split': param_range[1:]}]

	grid_params_svm = [{'clf__kernel': ['linear', 'rbf'], 
			'clf__C': param_range}]

	# Construct grid searches
	jobs = -1

	gs_lr = GridSearchCV(estimator=pipe_lr,
				param_grid=grid_params_lr,
				scoring='accuracy',
				cv=5)
				
	gs_lr_pca = GridSearchCV(estimator=pipe_lr_pca,
				param_grid=grid_params_lr,
				scoring='accuracy',
				cv=5)
				
	gs_rf = GridSearchCV(estimator=pipe_rf,
				param_grid=grid_params_rf,
				scoring='accuracy',
				cv=5, 
				n_jobs=jobs)

	gs_rf_pca = GridSearchCV(estimator=pipe_rf_pca,
				param_grid=grid_params_rf,
				scoring='accuracy',
				cv=5, 
				n_jobs=jobs)

	gs_svm = GridSearchCV(estimator=pipe_svm,
				param_grid=grid_params_svm,
				scoring='accuracy',
				cv=5,
				n_jobs=jobs)

	gs_svm_pca = GridSearchCV(estimator=pipe_svm_pca,
				param_grid=grid_params_svm,
				scoring='accuracy',
				cv=5,
				n_jobs=jobs)

	# List of pipelines for ease of iteration
	grids = [gs_lr, gs_lr_pca, gs_rf, gs_rf_pca, gs_svm, gs_svm_pca]

	# Dictionary of pipelines and classifier types for ease of reference
	grid_dict = {0: 'Logistic Regression', 1: 'Logistic Regression w/PCA', 
			2: 'Random Forest', 3: 'Random Forest w/PCA', 
			4: 'Support Vector Machine', 5: 'Support Vector Machine w/PCA'}

	# Fit the grid search objects
	print('Performing model optimizations comparisons...')
	result_dict={}
	for idx, gs in enumerate(grids):
		print('\nEstimator: %s' % grid_dict[idx])	
		# Fit grid search	
	
		gs.fit(X_train, y_train)
		# Best params
		print('Best params: %s' % gs.best_params_)
		# Best training data accuracy
		print('Best training accuracy: %.3f' % gs.best_score_)
		# Predict on test data with best params
		y_pred = gs.predict(X_test)
		# Test data accuracy of model with best params
		print('Test set accuracy score for best params: %.3f ' % accuracy_score(y_test, y_pred))
		# Add the result to the result dictionary
		result_dict[grid_dict[idx]] = {'Best Params':gs.best_params_, 'Best Training Accuracy':gs.best_score_, 'Test set accuracy score for best params':accuracy_score(y_test, y_pred)}

	return result_dict