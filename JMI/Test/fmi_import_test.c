/*
    Copyright (C) 2012 Modelon AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

#include <FMI1/fmi1_types.h>
#include <FMI1/fmi1_functions.h>
#include <Common/fmi_import_context.h>

void mylogger(fmi1_component_t c, fmi1_string_t instanceName, fmi1_status_t status, fmi1_string_t category, fmi1_string_t message, ...)
{
	char msg[2024];
	va_list argp;	
	va_start(argp, message);
	vsprintf(msg, message, argp);
	if (!instanceName) instanceName = "?";
	if (!category) category = "?";
	printf("fmiStatus = %d;  %s (%s): %s\n", status, instanceName, category, msg);
}

void do_exit(int code)
{
	printf("Press any key to exit\n");
	getchar();
	exit(code);
}

int main(int argc, char *argv[])
{
	fmi1_callback_functions_t callBackFunctions;
	const char* FMUPath;
	const char* tmpPath;
	const char* dllPath;
	const char* modelIdentifier;
	const char* modelName;
	const char* model_description_path;
	const char* instanceName;
	const char*  GUID;
	jm_callbacks callbacks;
	fmi_import_context_t* context;
	fmi_version_enu_t version;

	fmi1_import_t* fmu;

	if(argc < 3) {
		printf("Usage: %s <fmu_file> <temporary_dir>\n", argv[0]);
		do_exit(1);
	}

	FMUPath = argv[1];
	tmpPath = argv[2];


	callbacks.malloc = malloc;
    callbacks.calloc = calloc;
    callbacks.realloc = realloc;
    callbacks.free = free;
    callbacks.logger = mylogger;
    callbacks.context = 0;

	context = fmi_import_allocate_context(&callbacks);

#if 0
	if (jm_status_error == fmi_import_unzip(FMUPath, tmpPath)) {
		printf("Failed to unzip the FMU file\n");
		do_exit(1);
	}

	//version = fmi_import_get_fmi_version(context, tmpPath);

	//if(version != fmi_version_1_enu) {
	//	printf("Only version 1.0 is supported so far\n");
	//	do_exit(1);
	//}

	fmu = fmi1_import_parse_xml(context, tmpPath);

	if(!fmu) {
		printf("Error parsing XML, exiting\n");
		do_exit(1);
	}
	modelIdentifier = fmi1_import_get_model_identifier(fmu);
	modelName = fmi1_xml_get_model_name(fmu);
	GUID = fmi1_xml_get_GUID(fmu);

	printf("Model name: %s\n", modelName);
    printf("Model identifier: %s\n", modelIdentifier);
    printf("Model GUID: %s\n", GUID);

	status = fmi1_import_load_dll(fmu);

	if (status == jm_status_error) {
		printf("Could not load the dll\n");
		do_exit(1);
	}

	printf("Version returned from FMU:   %s\n", fmi1_import_get_version(fmu));

	fmi1_import_free(fmu);
	fmi_import_free_context(context);
	
	printf("Everything seems to be OK since you got this far=)!\n");

	do_exit(0);
#endif
}


